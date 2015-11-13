#-*- coding: utf-8 -*-
#QuickNav
#(C) 2015 Tuukka Ojala <tuukka.ojala@gmail.com>

import globalPluginHandler
import ui
import virtualBuffers

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "Quick nav"
    enabled = False
    last_state = False
    interceptor = None
    #Format is (script, rotor_label)
    modes = [
        ("Heading", "headings"), ("Link", "links"),
        ("FormField", "form fields"), ("BlockQuote", "block quotes"),
        ("Edit", "edit fields"), ("RadioButton", "radio buttons"),
        ("Table", "tables"), ("UnvisitedLink", "unvisited links"),
        ("ListItem", "list items"), ("EmbeddedObject", "embedded objects"),
        ("Annotation", "annotations"), ("Separator", "separators"),
        ("Landmark", "landmarks"), ("Graphic", "graphics"),
        ("List", "lists"), ("CheckBox", "check boxes"),
        ("ComboBox", "combo boxes"), ("VisitedLink", "visited links"),
        ("Button", "buttons"), ("NotLinkBlock", "Text after link block"),
        ("Frame", "frames"),
        ("moveByWord", "words"), ("moveByCharacter", "characters")]
    current_mode = 0
    prev_rotor_script = None
    next_rotor_script = None
    dynamic_gestures = {
        "kb:leftArrow": "moveLineUp",
        "kb:rightArrow": "moveLineDown",
        "kb:upArrow": "moveRotorUp",
        "kb:downArrow": "moveRotorDown",
        "kb:control+leftArrow": "cycleRotor",
        "kb:control+rightArrow": "cycleRotor",
    }
    
    def event_gainFocus(self, obj, nextHandler):
        """Makes it possible to activate / prevents the activation of quick nav based on the current object."""
        if obj is not None and isinstance(obj.treeInterceptor, virtualBuffers.VirtualBuffer):
            self.interceptor = obj.treeInterceptor
            if self.last_state:
                self.activate()
        else:
            self.interceptor = None
            if self.enabled:
                self.deactivate()
        nextHandler()

    def activate(self):
        """Activates quick nav."""
        self.bindGestures(self.dynamic_gestures)
        if not self.prev_rotor_script:
            self.update_rotor_scripts()
        self.enabled = True

    def deactivate(self):
        """Deactivates quick nav."""
        for gesture in self.dynamic_gestures.keys():
            self.removeGestureBinding(gesture)
        self.enabled = False

    def update_rotor_scripts(self):
        """Concatenates script names to be used with the current rotor setting."""
        script_name = self.modes[self.current_mode][0]
        #Jump by word/character scripts are named differently than quick nav keys, so handle those first.
        if script_name.startswith("move"):
            self.prev_rotor_script = "script_" + script_name + "_back"
            self.next_rotor_script = "script_" + script_name + "_forward"
        else:
            self.prev_rotor_script = "script_previous" + script_name
            self.next_rotor_script = "script_next" + script_name

    def script_toggleQuickNav(self, gesture):
        """Turns quick nav either on or off if possible."""
        if self.interceptor and not self.enabled:
            self.activate()
            self.last_state = True
            ui.message("Quick nav on")
        elif self.enabled:
            self.last_state = False
            self.deactivate()
            ui.message("Quick nav off")
        else:
            gesture.send()

    def script_moveLineUp(self, gesture):
        self.interceptor.script_moveByLine_back(gesture)

    def script_moveLineDown(self, gesture):
        self.interceptor.script_moveByLine_forward(gesture)

    def script_moveRotorUp(self, gesture):
        getattr(self.interceptor, self.prev_rotor_script)(gesture)

    def script_moveRotorDown(self, gesture):
        getattr(self.interceptor, self.next_rotor_script)(gesture)

    def script_cycleRotor(self, gesture):
        if gesture.mainKeyName == "leftArrow":
            self.current_mode -= 1
        elif gesture.mainKeyName == "rightArrow":
            self.current_mode += 1
        if self.current_mode < 0:
            self.current_mode = len(self.modes) -1
        elif self.current_mode >= len(self.modes):
            self.current_mode = 0
        self.update_rotor_scripts()
        mode_label = self.modes[self.current_mode][1]
        ui.message(mode_label)

    __gestures = {
        "kb:control+-": "toggleQuickNav",
    }