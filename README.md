# MOTD App

This repository contains a small Django application that displays
"messages of the day" (MOTDs) depending on which groups a logged in user
belongs to.  Each group can have its own MOTD defined via the `GroupMotd`
model.  The app provides a single view `motd_dashboard` that renders all
MOTDs relevant to the current user.  Messages can also be defined for
Alliance Auth states using the `StateMotd` model, allowing per-state
messages in addition to per-group ones.
