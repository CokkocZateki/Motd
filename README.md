# AA MOTD - Message of the Day for Alliance Auth

A simple and powerful Message of the Day (MOTD) app for Alliance Auth that displays important announcements and notifications on the dashboard.

- [AA Message of the Day](#aa-motd)
  - [Features](#features)
  - [Installation](#installation)
    - [Step 1 - Install the Package](#step1)
    - [Step 2 - Configure Alliance Auth](#step2)
    - [Step 3 - Add the Scheduled Tasks and Settings](#step3)
    - [Step 4 - Migration to AA](#step4)
    - [Step 5 - Setting up Permissions](#step5)

## Features <a name="features"></a>

- **Dashboard Widget**: Shows current MOTD messages on the main Alliance Auth dashboard
- **Flexible Scheduling**: Set start and end dates for messages
- **Group Restrictions**: Show messages only to specific groups or to all users
- **Multiple Styles**: Bootstrap alert styles (info, success, warning, danger)
- **Front-end Management**: Users with permission can add messages directly from the dashboard
- **Automatic Cleanup**: Management command to clean up expired messages

## Installation <a name="installation"></a>

> [!NOTE]
> AA MOTD System needs at least Alliance Auth v4.6.0
> Please make sure to update your Alliance Auth before you install this APP

1. Install the package:

Make sure you're in your virtual environment (venv) of your Alliance Auth then install the pakage.

```shell
pip install aa-motd
```

### Step 2 - Configure Alliance Auth<a name="step2"></a>

Configure your Alliance Auth settings (`local.py`) as follows:

- Add `'motd',` to `INSTALLED_APPS`

### Step 3 - Add the Scheduled Tasks<a name="step3"></a>

To set up the Scheduled Tasks add following code to your `local.py`

```python
CELERYBEAT_SCHEDULE["motd_update_all"] = {
    "task": "motd.tasks.update_all_motd",
    "schedule": crontab(minute="15,45"),
}
```

### Step 4 - Migration to AA<a name="step4"></a>

```shell
python manage.py collectstatic
python manage.py migrate
```

### Step 5 - Setting up Permissions<a name="step5"></a>

With the Following IDs you can set up the permissions for the Motd System

| ID              | Description                       |                                                             |
| :-------------- | :-------------------------------- | :---------------------------------------------------------- |
| `basic_access`  | Can access the MOTD System module | All Members with the Permission can access the Motd System. |
| `manage_access` | Can manage MOTD                   | Users with this permission can manage all.                  |

## Usage

1. **Creating Messages**: Use the "Add Message" button on the MOTD page (requires `motd.add_motdmessage`)
1. **Scheduling**: Set start and end dates to control when messages appear
1. **Targeting**: Use group restrictions to show messages only to specific groups
1. **Styling**: Choose appropriate priority levels and Bootstrap styles for visual impact
1. **Legacy Group/State Messages**: Visit `/motd/dashboard/` to view group- or state-specific MOTDs

## License

MIT License

> [!NOTE]
> Contributing
> You want to improve the project?
> Just Make a [Pull Request](https://github.com/CokkocZateki/aa-motd/pulls) with the Guidelines.
> We Using pre-commit
