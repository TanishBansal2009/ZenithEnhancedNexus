# ---- Interfaces ----
from interfaces.speech import zen_speak, greet
from interfaces.input import get_user_input, remove_wake_word, get_input
from interfaces.startup import load_data_in_background, check_and_install_requirements
from interfaces.gemini import ask_gemini

# ---- Features ----
from features.apps import webbrowser
from features.jokes import fetch_display_joke
from features.reminders import add_reminder, check_reminders, reminders
from features.expression import solve_expression, expression_interpretation
from features.weather import display_weather_updates, cities

# ---- Core ----
from core.users import handle_user, user, user_has_developer_access, load_profiles
from core.context import process_user_input, context
from core.states.study_mode import study_mode, handle_study_mode
from core.states.developer_mode import handle_developer_queries
from core.states.standby import standby_mode
from core.states.help import handle_help_mode
from core.logger import write_backend_log

# ---- Resources ----
from resources.dialogue_library import (
    developer_startup,
    developer_intro,
    thank_you_responses,
    developer_break,
    introduction_responses,
    responses_condition,
    chit_chat
)
from resources.utils.date import extract_date, fetch_significance, answer_date_significance, handle_time_date_queries
from resources.utils.basics import handle_condition, handle_personal_questions, handle_self_introduction
