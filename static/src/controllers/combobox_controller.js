/**
 * Project:     conneCTION
 * Name:        static/src/controllers/combobox_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-14
 * Description: ComboBox Controller
 */

import { Controller } from "@hotwired/stimulus";

/**
 * Combobox Controller
 * ---------------------------------
 * A controller which converts the select element
 * into a rich combobox using the [Slim Select](https://slimselectjs.com/)
 * library.
 */
export default class extends Controller {
  static values = {
    // These are passed directly through to slim-select.
    contentLocation: { type: String, default: undefined },
    contentPosition: { type: String, default: "absolute" },
  };

  #slimSelectModule = null;
  #canConnect = false;

  initialize() {
    // We dynamically import the module to save on the initial bundle size.
    Promise.allSettled([
      import("slim-select/styles"),
      import("slim-select"),
    ]).then(([_, slimSelect]) => {
      this.#slimSelectModule = slimSelect.value.default;
      this.#canConnect = true;
    });
  }

  connect() {
    this.#initializeSlimSelect();
  }

  disconnect() {
    this.slimSelect.destroy();
  }

  #initializeSlimSelect() {
    if (!this.#canConnect) {
      // We use a timeout loop to make sure the module is available
      // before we attempt to create it.
      setTimeout(this.#initializeSlimSelect.bind(this));
    } else {
      this.slimSelect = new this.#slimSelectModule({
        select: this.element,
        settings: {
          contentLocation: document.querySelector(this.contentLocationValue),
          contentPosition: this.contentPositionValue,
        },
      });
    }
  }
}
