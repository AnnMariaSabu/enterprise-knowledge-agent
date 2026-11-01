import config
import ollama
import config
print("Documents found:")

for path in config.DOCS_DIR.rglob("*"):
    if path.suffix in config.SUPPORTED_EXTENSIONS:
        print(" -", path.relative_to(config.DOCS_DIR))

print()
print("Asking", config.CHAT_MODEL, "to say hello...")

response = ollama.chat(
    model=config.CHAT_MODEL,
    messages=[{"role": "user", "content": "Say hello to Ann in one short sentence."}],
)

print("AI says:", response["message"]["content"])        