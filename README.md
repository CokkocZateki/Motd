# MOTD App

This repository contains a very small Django app that renders a
"message of the day" (MOTD) based on the groups a logged in user
belongs to. The `madashboard` application provides a single view
`motd_dashboard` that checks if the user is a member of the **Capital
Group** and renders a special template when appropriate.

The templates live in `madashboard/templates/madashboard/` and can be
extended to suit your needs. To use the app add `madashboard` to your
Django `INSTALLED_APPS` and include `madashboard.urls` in your project
URL configuration.
