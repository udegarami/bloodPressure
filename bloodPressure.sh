#!/bin/bash
streamlit run bloodPressure.py&> /dev/null &
STREAMLIT_PID=$!
wait $STREAMLIT_PID
