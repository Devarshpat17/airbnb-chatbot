import gradio as gr
from models import search, response_generator

def chat_fn(message, history):
    results = search.search(message, 'processed/index.faiss', 'processed/vectors.pkl')
    response = response_generator.generate_response(results, message)
    # Split response into cards for each property (assuming "--- Property" is the separator)
    cards = [card.strip() for card in response.split('--- Property') if card.strip()]
    # Format as Markdown cards
    md = ""
    for idx, card in enumerate(cards, 1):
        md += f"### Property {idx}\n"
        md += f"```\n{card}\n```\n"
    return md

with gr.Blocks(title="MongoDB Chatbot") as demo:
    gr.Markdown(
        """
        # MongoDB Chatbot
        Ask about Airbnb listings. Each response will show up to 3 matching properties.
        """
    )
    chatbot = gr.Chatbot(label="Chat", show_label=False)
    with gr.Row():
        msg = gr.Textbox(placeholder="Type your question...", show_label=False, scale=8)
        clear = gr.Button("New Chat", scale=1)
    def user(user_message, history):
        return "", history + [[user_message, None]]
    def bot(history):
        user_message = history[-1][0]
        bot_message = chat_fn(user_message, history)
        history[-1][1] = bot_message
        return history
    msg.submit(user, [msg, chatbot], [msg, chatbot]).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()