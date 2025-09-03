#!/usr/bin/env python3
"""
Voice Cloning Training Pipeline

This script handles the complete voice cloning training process:
1. Audio preprocessing and feature extraction
2. Voice embedding extraction using Resemblyzer
3. Model training using VITS, So-VITS-SVC, or Bark
4. Model evaluation and quality assessment
"""

import os
import sys
import argparse
import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import torch
import torchaudio
from tqdm import tqdm

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from models.resemblyzer_wrapper import ResemblyzerWrapper
from models.vits_wrapper import VITSWrapper
from models.so_vits_svc_wrapper import SoVITSSVCWrapper
from data.audio_preprocessing import AudioPreprocessor
from data.dataset import VoiceDataset
from utils.audio_utils import AudioUtils
from utils.model_utils import ModelUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceTrainingPipeline:
    """Main voice training pipeline class"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.output_dir = Path(config['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.audio_preprocessor = AudioPreprocessor(config['audio'])
        self.voice_encoder = ResemblyzerWrapper(device=self.device)
        
        # Initialize model based on type
        self.model_type = config['model']['type']
        if self.model_type == 'vits':
            self.model = VITSWrapper(config['model'], device=self.device)
        elif self.model_type == 'so-vits-svc':
            self.model = SoVITSSVCWrapper(config['model'], device=self.device)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
        
        # Training state
        self.training_history = {
            'loss': [],
            'val_loss': [],
            'epochs': [],
            'best_loss': float('inf')
        }
    
    def preprocess_audio(self, audio_files: List[str]) -> Tuple[List[str], Dict]:
        """Preprocess audio files and extract features"""
        logger.info("Starting audio preprocessing...")
        
        processed_files = []
        preprocessing_stats = {
            'total_files': len(audio_files),
            'processed_files': 0,
            'failed_files': 0,
            'total_duration': 0.0,
            'quality_scores': []
        }
        
        for audio_file in tqdm(audio_files, desc="Preprocessing audio"):
            try:
                # Process audio file
                processed_file = self.audio_preprocessor.process_file(audio_file)
                if processed_file:
                    processed_files.append(processed_file)
                    preprocessing_stats['processed_files'] += 1
                    
                    # Get audio duration and quality
                    duration = AudioUtils.get_audio_duration(processed_file)
                    quality_score = AudioUtils.assess_audio_quality(processed_file)
                    
                    preprocessing_stats['total_duration'] += duration
                    preprocessing_stats['quality_scores'].append(quality_score)
                    
                    logger.info(f"Processed: {audio_file} (duration: {duration:.2f}s, quality: {quality_score:.2f})")
                else:
                    preprocessing_stats['failed_files'] += 1
                    logger.warning(f"Failed to process: {audio_file}")
            
            except Exception as e:
                preprocessing_stats['failed_files'] += 1
                logger.error(f"Error processing {audio_file}: {str(e)}")
        
        # Calculate average quality
        if preprocessing_stats['quality_scores']:
            preprocessing_stats['avg_quality'] = np.mean(preprocessing_stats['quality_scores'])
            preprocessing_stats['min_quality'] = np.min(preprocessing_stats['quality_scores'])
            preprocessing_stats['max_quality'] = np.max(preprocessing_stats['quality_scores'])
        
        logger.info(f"Preprocessing completed: {preprocessing_stats['processed_files']}/{preprocessing_stats['total_files']} files processed")
        return processed_files, preprocessing_stats
    
    def extract_voice_embeddings(self, audio_files: List[str]) -> Tuple[np.ndarray, Dict]:
        """Extract voice embeddings using Resemblyzer"""
        logger.info("Extracting voice embeddings...")
        
        embeddings = []
        embedding_stats = {
            'total_files': len(audio_files),
            'successful_extractions': 0,
            'failed_extractions': 0,
            'embedding_dim': None
        }
        
        for audio_file in tqdm(audio_files, desc="Extracting embeddings"):
            try:
                embedding = self.voice_encoder.extract_embedding(audio_file)
                if embedding is not None:
                    embeddings.append(embedding)
                    embedding_stats['successful_extractions'] += 1
                    
                    if embedding_stats['embedding_dim'] is None:
                        embedding_stats['embedding_dim'] = embedding.shape[0]
                else:
                    embedding_stats['failed_extractions'] += 1
                    logger.warning(f"Failed to extract embedding from: {audio_file}")
            
            except Exception as e:
                embedding_stats['failed_extractions'] += 1
                logger.error(f"Error extracting embedding from {audio_file}: {str(e)}")
        
        if embeddings:
            embeddings_array = np.array(embeddings)
            logger.info(f"Embedding extraction completed: {embedding_stats['successful_extractions']}/{embedding_stats['total_files']} successful")
            return embeddings_array, embedding_stats
        else:
            raise RuntimeError("No voice embeddings could be extracted")
    
    def prepare_dataset(self, audio_files: List[str], embeddings: np.ndarray) -> VoiceDataset:
        """Prepare dataset for training"""
        logger.info("Preparing training dataset...")
        
        # Create dataset
        dataset = VoiceDataset(
            audio_files=audio_files,
            embeddings=embeddings,
            config=self.config['dataset']
        )
        
        logger.info(f"Dataset prepared: {len(dataset)} samples")
        return dataset
    
    def train_model(self, dataset: VoiceDataset) -> Dict:
        """Train the voice cloning model"""
        logger.info(f"Starting model training with {self.model_type}...")
        
        # Split dataset
        train_size = int(0.8 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
        
        logger.info(f"Training samples: {len(train_dataset)}, Validation samples: {len(val_dataset)}")
        
        # Train model
        training_results = self.model.train(
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            config=self.config['training']
        )
        
        # Update training history
        self.training_history['loss'].extend(training_results['train_loss'])
        self.training_history['val_loss'].extend(training_results['val_loss'])
        self.training_history['epochs'].extend(range(len(training_results['train_loss'])))
        
        if training_results['best_val_loss'] < self.training_history['best_loss']:
            self.training_history['best_loss'] = training_results['best_val_loss']
        
        logger.info("Model training completed")
        return training_results
    
    def evaluate_model(self, test_dataset: VoiceDataset) -> Dict:
        """Evaluate the trained model"""
        logger.info("Evaluating trained model...")
        
        evaluation_results = self.model.evaluate(test_dataset)
        
        logger.info(f"Model evaluation completed. Quality score: {evaluation_results['quality_score']:.2f}/10")
        return evaluation_results
    
    def save_model(self, model_path: str) -> str:
        """Save the trained model"""
        logger.info("Saving trained model...")
        
        model_file = self.model.save_model(model_path)
        logger.info(f"Model saved to: {model_file}")
        return model_file
    
    def generate_sample(self, text: str, output_path: str) -> str:
        """Generate a sample audio using the trained model"""
        logger.info(f"Generating sample audio: {text}")
        
        try:
            audio_path = self.model.generate_speech(text, output_path)
            logger.info(f"Sample audio generated: {audio_path}")
            return audio_path
        except Exception as e:
            logger.error(f"Error generating sample audio: {str(e)}")
            raise
    
    def run_training_pipeline(self, audio_files: List[str], text_samples: List[str]) -> Dict:
        """Run the complete training pipeline"""
        start_time = time.time()
        
        try:
            # Step 1: Audio preprocessing
            processed_files, preprocessing_stats = self.preprocess_audio(audio_files)
            
            if not processed_files:
                raise RuntimeError("No audio files could be processed")
            
            # Step 2: Voice embedding extraction
            embeddings, embedding_stats = self.extract_voice_embeddings(processed_files)
            
            # Step 3: Dataset preparation
            dataset = self.prepare_dataset(processed_files, embeddings)
            
            # Step 4: Model training
            training_results = self.train_model(dataset)
            
            # Step 5: Model evaluation
            evaluation_results = self.evaluate_model(dataset)
            
            # Step 6: Save model
            model_path = str(self.output_dir / f"{self.model_type}_model.pth")
            saved_model_path = self.save_model(model_path)
            
            # Step 7: Generate sample audio
            sample_audio_path = None
            if text_samples:
                sample_text = text_samples[0]
                sample_output = str(self.output_dir / "sample_audio.wav")
                sample_audio_path = self.generate_sample(sample_text, sample_output)
            
            # Compile results
            pipeline_results = {
                'success': True,
                'model_path': saved_model_path,
                'sample_audio_path': sample_audio_path,
                'preprocessing_stats': preprocessing_stats,
                'embedding_stats': embedding_stats,
                'training_results': training_results,
                'evaluation_results': evaluation_results,
                'training_history': self.training_history,
                'total_training_time': time.time() - start_time
            }
            
            # Save results to file
            results_file = self.output_dir / "training_results.json"
            with open(results_file, 'w') as f:
                json.dump(pipeline_results, f, indent=2, default=str)
            
            logger.info("Training pipeline completed successfully!")
            return pipeline_results
        
        except Exception as e:
            logger.error(f"Training pipeline failed: {str(e)}")
            raise


def load_config(config_path: str) -> Dict:
    """Load configuration from file"""
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main training script"""
    parser = argparse.ArgumentParser(description="Voice Cloning Training Pipeline")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    parser.add_argument("--audio_dir", required=True, help="Directory containing audio files")
    parser.add_argument("--output_dir", required=True, help="Output directory for trained model")
    parser.add_argument("--text_samples", nargs="+", help="Sample texts for testing")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    config['output_dir'] = args.output_dir
    
    # Get audio files
    audio_dir = Path(args.audio_dir)
    audio_files = list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3")) + list(audio_dir.glob("*.flac"))
    audio_files = [str(f) for f in audio_files]
    
    if not audio_files:
        logger.error(f"No audio files found in {audio_dir}")
        sys.exit(1)
    
    logger.info(f"Found {len(audio_files)} audio files")
    
    # Initialize pipeline
    pipeline = VoiceTrainingPipeline(config)
    
    # Run training
    try:
        results = pipeline.run_training_pipeline(audio_files, args.text_samples or [])
        
        # Print summary
        print("\n" + "="*50)
        print("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
        print("="*50)
        print(f"Model saved to: {results['model_path']}")
        print(f"Quality score: {results['evaluation_results']['quality_score']:.2f}/10")
        print(f"Total training time: {results['total_training_time']/3600:.2f} hours")
        print(f"Processed {results['preprocessing_stats']['processed_files']} audio files")
        print(f"Total audio duration: {results['preprocessing_stats']['total_duration']/60:.2f} minutes")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()