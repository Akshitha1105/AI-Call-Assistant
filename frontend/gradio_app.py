import gradio as gr
import requests
import os

API_BASE = os.environ.get("API_BASE", "http://localhost:8000/api")


def login(email, password):
    data = {"username": email, "password": password}
    r = requests.post(f"{API_BASE}/auth/login", data=data)
    if r.status_code != 200:
        return None, f"Login failed: {r.text}"
    token = r.json()["access_token"]
    return token, "Logged in"


def signup(email, password):
    r = requests.post(f"{API_BASE}/auth/signup", json={"email": email, "password": password})
    if r.status_code != 200:
        return f"Signup failed: {r.text}"
    return "Signup successful. Please login."


def list_voices(token):
    r = requests.get(f"{API_BASE}/voices/list_voices", headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        return []
    voices = r.json()
    return [f"{v['id']} - {v['name']}" for v in voices]


def upload_voice(token, name, description, files):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "description": description}
    files_field = [("files", (f.name, f.read(), f"audio/{f.name.split('.')[-1]}")) for f in files]
    r = requests.post(f"{API_BASE}/voices/upload_voice", headers=headers, data=data, files=files_field)
    if r.status_code != 200:
        return f"Upload failed: {r.text}"
    return "Voice uploaded."


def generate(token, voice_choice, text, language):
    if not voice_choice:
        return None, "Select a voice"
    voice_id = int(voice_choice.split(" - ")[0])
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(
        f"{API_BASE}/tts/generate_speech",
        headers=headers,
        json={"voice_id": voice_id, "text": text, "language": language or None},
    )
    if r.status_code != 200:
        return None, f"TTS failed: {r.text}"
    return (22050, r.content), "Success"


with gr.Blocks(title="AI Voice Platform") as demo:
    gr.Markdown("**AI Voice Platform** - login, upload voice, and generate speech.")

    with gr.Tab("Auth"):
        email = gr.Textbox(label="Email")
        password = gr.Textbox(label="Password", type="password")
        token_state = gr.State(value="")

        login_btn = gr.Button("Login")
        signup_btn = gr.Button("Signup")
        auth_status = gr.Markdown()

        login_btn.click(login, inputs=[email, password], outputs=[token_state, auth_status])
        signup_btn.click(signup, inputs=[email, password], outputs=[auth_status])

    with gr.Tab("Upload Voice"):
        name = gr.Textbox(label="Voice Name")
        desc = gr.Textbox(label="Description")
        files = gr.File(label="Audio Files", file_count="multiple", type="filepath")
        up_status = gr.Markdown()

        def upload_wrapper(token, name, desc, paths):
            opened = [open(p, "rb") for p in (paths or [])]
            try:
                return upload_voice(token, name, desc, opened)
            finally:
                for f in opened:
                    try:
                        f.close()
                    except Exception:
                        pass

        up_btn = gr.Button("Upload")
        up_btn.click(upload_wrapper, inputs=[token_state, name, desc, files], outputs=[up_status])

    with gr.Tab("Generate"):
        refresh_btn = gr.Button("Refresh Voices")
        voices_dd = gr.Dropdown(label="Voices", choices=[])
        text = gr.Textbox(label="Text")
        lang = gr.Textbox(label="Language (optional, e.g., 'en')")
        gen_btn = gr.Button("Generate")
        audio = gr.Audio(label="Output", type="numpy")
        gen_status = gr.Markdown()

        def refresh(token):
            return gr.update(choices=list_voices(token))

        refresh_btn.click(refresh, inputs=[token_state], outputs=[voices_dd])
        gen_btn.click(generate, inputs=[token_state, voices_dd, text, lang], outputs=[audio, gen_status])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)

