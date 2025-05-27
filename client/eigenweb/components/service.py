import streamlit as st
from . import are_you_sure
from time import sleep
from eigen import ServiceStatus

def run_with_lock(service, func):
    """
    Decorator to run a service function with a lock to prevent concurrent modifications.

    :param service: The service instance to run the function on.
    :param func: The function to run on the service.
    """
    def wrapper(*args, **kwargs):
        with service.lock:
            return func(*args, **kwargs)
    return wrapper

def service_card_head(slug, service):
    with st.container():
        left_row, right_row = st.columns([1, 3])
        with left_row:
            st.image(service.config.info.icon)
        with right_row:
            st.markdown(f"### {service.config.info.name}")
            st.markdown(service.config.info.description)

def service_controls(slug, service, status, busy):
    col1, col2, col3, col4, _ = st.columns([2, 2, 2, 2, 1])
    corrupted = status in [ServiceStatus.NOT_FOUND, ServiceStatus.UNKNOWN, ServiceStatus.ERROR]
    stopped = status in [ServiceStatus.STOPPED, ServiceStatus.NOT_FOUND]
    alive = status in [ServiceStatus.RUNNING, ServiceStatus.RESTARTING, ServiceStatus.PAUSED]

    if not service.is_installed():
        with col4:
            st.button(
                "",
                icon=":material/downloading:",
                type="tertiary",
                key=f"install_{slug}",
                disabled=busy or alive,
                on_click=run_with_lock(service, service.install),
            )
        return

    with col1:
        st.button(
            "",
            icon=":material/play_circle:",
            type="tertiary",
            key=f"start_{slug}",
            disabled=alive or busy or corrupted,
            on_click=run_with_lock(service, service.start),
        )
    with col2:
        st.button(
            "",
            icon=":material/refresh:",
            type="tertiary",
            key=f"restart_{slug}",
            disabled=stopped or status in [ServiceStatus.RESTARTING] or busy or corrupted,
            on_click=run_with_lock(service, service.restart),
        )
    with col3:
        st.button(
            "",
            icon=":material/stop_circle:",
            type="tertiary",
            key=f"stop_{slug}",
            disabled=stopped or busy or corrupted,
            on_click=run_with_lock(service, service.stop),
        )
    with col4:
        def uninstall_service():
            def perform_uninstall():
                run_with_lock(service, service.uninstall)()
                st.toast(f"Service `{service.config.info.name}` uninstalled successfully.", icon=":material/check_circle:")
            are_you_sure(
                message=f"Are you sure you want to uninstall the service `{service.config.info.name}`?",
                confirm="Uninstall",
                key=f"uninstall_{slug}",
                callback=perform_uninstall,
            )

        st.button(
            "",
            icon=":material/delete:",
            type="tertiary",
            key=f"uninstall_{slug}",
            disabled=busy or alive,
            on_click=uninstall_service,
        )

def service_badge(status, busy, installed):
    if busy:
        st.badge("Busy", icon=":material/hourglass_top:", color="grey")
        return
    if not installed:
        st.badge("Not Installed", icon=":material/help:", color="violet")
        return
    match(status):
        case ServiceStatus.RUNNING:
            st.badge("Running", icon=":material/check_circle:", color="green")
        case ServiceStatus.STOPPED:
            st.badge("Stopped", icon=":material/stop_circle:", color="red")
        case ServiceStatus.RESTARTING:
            st.badge("Restarting", icon=":material/restart_alt:", color="orange")
        case ServiceStatus.PAUSED:
            st.badge("Paused", icon=":material/pending:", color="yellow")
        case ServiceStatus.ERROR:
            st.badge("Error", icon=":material/error_circle:", color="red")
        case ServiceStatus.UPDATING:
            st.badge("Updating", icon=":material/downloading:", color="blue")
        case ServiceStatus.NOT_FOUND:
            st.badge("Not Found", icon=":material/help:", color="violet")
        case ServiceStatus.UNKNOWN:
            st.badge("Unknown", icon=":material/shield_question:", color="red")
        case _:
            st.exception(f"Unknown status: {status}")

@st.fragment(run_every="3s")
def service(slug, service):
    """
    Renders a service card with its status and control buttons.

    :param slug: The unique identifier for the service.
    :param service: The service instance to display.
    """
    service_status = service.status
    service_busy = service.is_busy()
    service_installed = service.is_installed()

    if "callback_queue" not in st.session_state:
        st.session_state.callback_queue = []

    while st.session_state.callback_queue:
        st.session_state.callback_queue.pop(0)()

    with st.container(border=True):
        with st.container():
            left_row, right_row = st.columns([1, 3])
            with left_row:
                st.image(service.config.info.icon)
            with right_row:
                st.markdown(f"### {service.config.info.name}")
                st.markdown(service.config.info.description)

        with st.container():
            col1, col2, col3 = st.columns([3, 5, 2])
            with col1:
                service_badge(service_status, service_busy, service_installed)
            with col3:
                service_controls(slug, service, service_status, service_busy)
