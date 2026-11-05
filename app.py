import streamlit as st
import chess
import base64

st.set_page_config(page_title="Streamlit Chess", page_icon="♟️", layout="centered")

# Initialize game state
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

board = st.session_state.board

st.title("♟️ Python Chess in Streamlit")
st.write("Play a game of chess locally by entering your moves below!")

# Reset button in sidebar
with st.sidebar:
    st.header("Game Controls")
    if st.button("🔄 New Game"):
        st.session_state.board = chess.Board()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Rules & Help")
    st.write("Enter moves in **SAN** format (e.g., `e4`, `Nf3`, `O-O`) or **UCI** format (e.g., `e2e4`).")

# Render board as SVG
def render_board(board_obj):
    svg = chess.svg.board(board_obj, size=400)
    encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f'<img src="data:image/svg+xml;base64,{encoded}" width="400"/>'

# Layout columns
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(render_board(board), unsafe_allow_html=True)

with col2:
    st.subheader("Game Status")
    
    # Check game status
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        st.error(f"🏁 **Checkmate! {winner} wins!**")
    elif board.is_stalemate():
        st.warning("🤝 **Draw by stalemate!**")
    elif board.is_check():
        st.warning("⚠️ **Check!**")
    else:
        turn_str = "White's turn" if board.turn == chess.WHITE else "Black's turn"
        st.info(f"Current turn: **{turn_str}**")

    # Move input form
    with st.form(key="move_form", clear_on_submit=True):
        move_input = st.text_input("Enter Move (e.g. e4, Nf3):")
        submit_button = st.form_submit_button(label="Play Move")

        if submit_button and move_input:
            move_input = move_input.strip()
            try:
                # Try parsing as SAN (Standard Algebraic Notation) first, then UCI
                move = board.parse_san(move_input)
            except ValueError:
                try:
                    move = chess.Move.from_uci(move_input)
                except ValueError:
                    move = None

            if move and move in board.legal_moves:
                board.push(move)
                st.rerun()
            else:
                st.error("❌ Invalid move! Check notation or legality.")

    # Move history
    st.markdown("### Move History")
    move_stack = board.move_stack
    if move_stack:
        history_text = ""
        temp_board = chess.Board()
        for i, m in enumerate(move_stack):
            san_move = temp_board.san(m)
            temp_board.push(m)
            if i % 2 == 0:
                history_text += f"{i//2 + 1}. {san_move} "
            else:
                history_text += f"{san_move}  "
        st.text_area("Moves:", value=history_text, height=100, disabled=True)
    else:
        st.write("No moves played yet.")
