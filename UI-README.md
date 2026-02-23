Use the following CLI commands to launch the UI.
- UI allows you to drag-drop PDF file, encrypt it(password protect it) and then, download it.

Commands to run:
```shell
uv sync --all-groups
uv pip install -r requirements-webui.txt
uv pip install -e .
uv run streamlit run app/streamlit_app.py
```
Then,
Open:
http://localhost:8501/

Screenshot:
<img width="1112" height="839" alt="image" src="https://github.com/user-attachments/assets/a5fdbe30-052e-4176-8abc-21a8c589f557" />
