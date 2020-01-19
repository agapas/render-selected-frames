# render-selected-frames
Simple addon for blender 3d to render selected frames. The result images are saved with the settings from the animation output.

### Blender version:
Made and tested on Blender 2.80 (windows64).
If you need version for Blender 2.79 or older, check the link: [render-selected-frames-blender2.79](https://github.com/agapas/render-selected-frames-blender2.79)

### More info

Input frames can be set like in example: '1,3-5,10,7',<br/>so in this case following frames will be rendered: 1, 3, 4, 5, 7, 10.

<img src="https://raw.githubusercontent.com/agapas/render-selected-frames/master/images/1.png" width="340" height="695"/>

*Notes:*
* frames order is not important
* please don't use spaces between input frames, just commas
* toggle system console to see addon's raport with output paths and rendering and saving times

### Installing

* go to: File/User Preferences/Add-ons and click 'Install Add-on from File...'
* select the ZIP you downloaded and click 'Install Add-on from File...'
* enable the addon
* save user settings to keep addon enabled over multiple blender sessions

## License

This project is licensed under the [GNU v3.0] License - see the [LICENSE.md](LICENSE) file for details.
