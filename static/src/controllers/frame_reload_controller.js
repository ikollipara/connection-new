/**
 * Project:     conneCTION
 * Name:        static/src/controllers/frame_reload_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-21
 * Description: Force Reload a Controller
 */

import { Controller } from "@hotwired/stimulus";

/**
 * Frame Reload Controller
 * ------------------------------
 * A controller to enable dynamic reloading of a Turbo Frame.
 */
export default class extends Controller {
  reload() {
    this.element.reload();
  }
}
