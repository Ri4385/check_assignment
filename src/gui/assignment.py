import streamlit as st

def main() -> None:

    if "session" not in st.session_state:
        st.session_state.session = False

    if not st.session_state.session:
        st.write("plz login")
        return

    st.button("get assignment")
    return

if __name__ == "__main__":
    main()