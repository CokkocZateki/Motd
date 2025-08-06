
# AA MOTD - Message of the Day for Alliance Auth

A simple and powerful Message of the Day (MOTD) app for Alliance Auth that displays important announcements and notifications on the dashboard.

## Features

- **Dashboard Widget**: Shows current MOTD messages on the main Alliance Auth dashboard
- **Priority System**: Critical, High, Normal, and Low priority messages with visual indicators
- **Flexible Scheduling**: Set start and end dates for messages
- **Group Restrictions**: Show messages only to specific groups or to all users
- **Multiple Styles**: Bootstrap alert styles (info, success, warning, danger)
- **Admin Interface**: Easy-to-use Django admin interface for managing messages
- **Automatic Cleanup**: Management command to clean up expired messages
- **Persistent Display**: Messages cannot be dismissed and remain until they expire or are deactivated

## Installation

1. Install the package:
```bash
pip install aa-motd
```

2. Add to your Alliance Auth settings in `local.py`:
```python
INSTALLED_APPS += [
    'motd',
]
```

3. Run migrations:
```bash
python manage.py migrate
python manage.py collectstatic
```

4. Restart your Alliance Auth services.

## Configuration

### Dashboard Widget Integration

To display the MOTD widget on your dashboard, you'll need to modify your main dashboard template to include the widget. Add this to your dashboard template:

```html
{% include 'motd/dashboard_widget.html' %}
```

### Permissions

The app uses the following permissions:
- `motd.view_motdmessage` - View MOTD messages
- `motd.add_motdmessage` - Create MOTD messages  
- `motd.change_motdmessage` - Edit MOTD messages
- `motd.delete_motdmessage` - Delete MOTD messages

Assign these permissions through the Alliance Auth admin interface.

### Cleanup Command

Set up a periodic task to clean up expired messages:

```bash
# Add to your crontab
0 2 * * * cd /path/to/your/allianceauth && python manage.py motd_cleanup
```

## Usage

1. **Creating Messages**: Go to the Django admin interface and create new MOTD messages
2. **Scheduling**: Set start and end dates to control when messages appear
3. **Targeting**: Use group restrictions to show messages only to specific groups
4. **Styling**: Choose appropriate priority levels and Bootstrap styles for visual impact

## Message Priorities

- **Critical**: Red warning icon, highest priority
- **High**: Orange exclamation, high priority  
- **Normal**: Blue bullhorn, standard priority
- **Low**: Gray info icon, lowest priority

## Requirements

- Alliance Auth >= 4.0.0
- Django >= 4.0
- Python >= 3.8

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
=======
# MOTD App



The templates live in `motd/templates/motd/` and can be
extended to suit your needs.  To use the app add `motd` to your
`INSTALLED_APPS` and include `motd.urls` in your project URL
configuration.  MOTDs can be managed through the Django admin interface.

After installing the app, run `python manage.py migrate` to create the
database tables for storing MOTDs.
