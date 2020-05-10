# render-selected-frames
Simple addon for blender 3d to render selected frames. The result images are saved with the settings from the animation output.

### Blender version:
Made and tested on Blender 2.80 (windows64).
If you need version for Blender 2.79 or older, check the link: [render-selected-frames-blender2.79](https://github.com/agapas/render-selected-frames-blender2.79)

### More info

Input frames can be set like in example: '1,3-5,10,7', so in this case following frames will be rendered: 1, 3, 4, 5, 7, 10.

<img src="https://raw.githubusercontent.com/agapas/render-selected-frames/master/images/ui.png" width="340" height="695"/>

### Notes and practical advices:

* frames order is not important
* do not set too many frames to render at once (it can be time and memory consuming)
* after pressing "Render Frames" button please wait a little bit for the addon to start
* use "Esc" (keyboard button) to stop rendering on the current frame
* toggle system console (after render is finished) to see addon's raport with output paths, rendering times and saving times
* you can open the output folder to see the progress during rendering

### Installing

* go to: Edit/Preferences/Add-ons and click 'Install Add-on'
* select the ZIP you downloaded and click button 'Install Add-on'
* enable the addon
* save preferences to keep addon enabled over multiple blender sessions

#### Installation note:

If the steps above don't work, try:
  * download just the "render_selected_frames.py" file<br/>
  * and save it into addons directory in your Blender path, for example into:<br/>
    C:\Program Files\Blender Foundation\Blender 2.82\2.82\scripts\addons
  * enable the addon in Blender's Edit/Preferences/Add-ons

## License

This project is licensed under the [GNU v3.0] License - see the [LICENSE.md](LICENSE) file for details.
