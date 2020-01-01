# FOLDSettings

Python script to Save settings in a local database

This directory contains a script, ```drive.py```, for push and restore your Files

## Configuring

it's easy to set up

All the configuration is done in a file named ```.config.ini``` stored at the root of your home folder.

To configure this script, create a file named ```.config.ini``` in your home directory.

In the file ```~/.config.ini```. add the files names to allow in the `[FILES_TO_SYNC]` section That you want to save in database, one by line.

```ini
[FILES_TO_SYNC]
~/.bash_profile
~/.config.ini
~/.gitconfig
~/.gitignore
~/.inputrc
~/.vimrc
~/.vim/colors/ayu.vim
~/.zshrc
~/init/resetup.sh
~/init/cleaner.sh
~/Library/Application Support/Code/User/settings.json
~/Library/Preferences/com.googlecode.iterm2.plist
~/Library/Fonts/Roboto Mono for Powerline.ttf
```

## Running

After the configuration file you now can run the script

```
$ python3 drive.py --help
```

## Note

The database name is ```locale.db```. stored at the root of your repository