# MOTD App

This repository contains a small Django application that displays
"messages of the day" (MOTDs) depending on which groups a logged in user
belongs to.  Each group can have its own MOTD defined via the `GroupMotd`
model.  The app provides a single view `motd_dashboard` that renders all
MOTDs relevant to the current user.  Messages can also be defined for
Alliance Auth states using the `StateMotd` model, allowing per-state
messages in addition to per-group ones.

The templates live in `motd/templates/motd/` and can be
extended to suit your needs.  To use the app add `motd` to your
`INSTALLED_APPS` and include `motd.urls` in your project URL
configuration.  MOTDs can be managed through the Django admin interface.

After installing the app, run `python manage.py migrate` to create the
database tables for storing MOTDs.
