# Home Assistant Add-on: Visitor Management System

## Installation

Follow these steps to get the add-on installed on your system:

1. Navigate in your Home Assistant frontend to **Settings** → **Add-ons** → **Add-on Store**.
2. Click the 3-dots menu at upper right **...** → **Repositories** and add this repository's URL: `https://github.com/goatboynz/HA-VMS`
3. The repository will now appear under "Local add-ons"
4. Click on "Visitor Management System" → **Install**

## How to use

1. Start the add-on
2. Check the logs of the add-on to see if everything went well
3. Open the Web UI or navigate to `http://homeassistant.local:8080`

## Configuration

**Note**: _Remember to restart the add-on when the configuration is changed._

Example add-on configuration:

```yaml
admin_username: admin
admin_password: your_secure_password_here
database_path: /data/visitors.db
max_file_size: 10485760
```

**Note**: _This is just an example, don't copy and paste it! Create your own!_

### Option: `admin_username`

The username for accessing the admin backend.

### Option: `admin_password`

The password for accessing the admin backend. **Change this from the default!**

### Option: `database_path`

The path where the SQLite database will be stored. Default is `/data/visitors.db`.

### Option: `max_file_size`

Maximum file size for photo uploads in bytes. Default is 10MB (10485760 bytes).

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality.

Releases are based on [Semantic Versioning][semver], and use the format
of `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented
based on the following:

- `MAJOR`: Incompatible or major changes.
- `MINOR`: Backwards-compatible new features and enhancements.
- `PATCH`: Backwards-compatible bugfixes and package updates.

## Support

Got questions?

You have several options to get them answered:

- The [Home Assistant Community Add-ons Discord chat server][discord] for add-on
  support and feature requests.
- The [Home Assistant Discord chat server][discord-ha] for general Home
  Assistant discussions and questions.
- The Home Assistant [Community Forum][forum].
- Join the [Reddit subreddit][reddit] in [/r/homeassistant][reddit]

You could also [open an issue here][issue] GitHub.

## Authors & contributors

The original setup of this repository is by [goatboynz][goatboynz].

## License

MIT License

Copyright (c) 2025 goatboynz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[discord-ha]: https://discord.gg/c5DvZ4e
[discord]: https://discord.me/hassioaddons
[forum]: https://community.home-assistant.io/t/repository-community-hass-io-add-ons/24705?u=frenck
[goatboynz]: https://github.com/goatboynz
[issue]: https://github.com/goatboynz/HA-VMS/issues
[reddit]: https://reddit.com/r/homeassistant
[releases]: https://github.com/goatboynz/HA-VMS/releases
[semver]: http://semver.org/spec/v2.0.0.html