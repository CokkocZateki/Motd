# MOTD App

This repository contains a small Django application that displays
"messages of the day" (MOTDs) depending on which groups a logged in user
belongs to.  Each group can have its own MOTD defined via the `GroupMotd`
model.  The app provides a single view `motd_dashboard` that renders all
MOTDs relevant to the current user.

The templates live in `madashboard/templates/madashboard/` and can be
extended to suit your needs.  To use the app add `madashboard` to your
`INSTALLED_APPS` and include `madashboard.urls` in your project URL
configuration.  MOTDs can be managed through the Django admin interface.
