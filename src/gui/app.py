import streamlit as st
import assignment

def main() -> None:
    st.title("PandA for the Lazy")

    if "session" not in st.session_state:
        st.session_state.session = False

    if not st.session_state.session:
        if st.button("login"):
            st.session_state.session = True
            st.rerun()
    else:
        if st.button("log out"):
            st.session_state.session = False
            st.rerun()

        tab_assignment, tab_resources = st.tabs(["assignment viewer", "resources downloader"])

        with tab_assignment:
            assignment.main()
        with tab_resources:
            st.write("resources downloader")
    return

if __name__ == "__main__":
    main()