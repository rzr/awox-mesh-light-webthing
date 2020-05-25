// -*- mode: js; js-indent-level:2;  -*-
// SPDX-License-Identifier: MIT
AFRAME.registerComponent('properties', {
 
  update: function(old) {
    var properties = this.data;
    for (var property of Object.keys(properties)) {
      switch(property) {
      case 'brightness':
        this.el.setAttribute('material', 'roughness',
                             this.data[property] / 100.);
        break;
      case 'on':
        this.el.setAttribute('color',
                             this.data[property] ? 'white' : '#A0A0A0');
        break;
      case 'color':
        if (this.data.on) {
          this.el.setAttribute(property, this.data[property]);
        }
        break;
      default:
        this.el.setAttribute(property,
                             this.data[property]);
        break;
      }
    }
  }
});
