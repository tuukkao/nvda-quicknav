# nvda-quicknav
OsX-style internet browsing for your Windows screen reader.
## Description
This is an add-on for the [NVDA screen reader][1] that implements a set of commands for browsing web content similar to VoiceOver's quick navigation feature. It lets you browse a web document by its elements with just the arrow keys (and some modifiers).
## Installation
Just throw [quickNav.py] into the globalPlugins directory of your NVDA installation.
## Usage
Press ctrl+- to toggle quick navigation on or off. When quick navigation is on, left anv right arrow keys are used to move on the page line by line, whereas up and down arrow keys move by the selected element (headings by default). The active element can be selected with ctrl+left arrow and ctrl+right arrow. You can move by all the elements supported by the conventional quick navigation keys as well as by word and character.
## Todo
* A dialog for reordering/hiding element types.
## Author
Tuukka Ojala <tuukka.ojala@gmail.com>
## License
This work is licensed under [the MIT license](LICENSE).

[1]: http://nvaccess.org