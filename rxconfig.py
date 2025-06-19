import reflex as rx

config = rx.Config(
    app_name="app",
    loglevel="default",
    show_built_with_reflex=False,
    is_reflex_cloud=False,
    # tailwind=None,
    plugins=[rx.plugins.TailwindV3Plugin()],
)
