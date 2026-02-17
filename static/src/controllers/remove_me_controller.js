/**
 * Project:     conneCTION
 * Name:        static/src/controllers/remove_me_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-12-03
 * Description: Remove the given element
 */

import { Controller } from "@hotwired/stimulus";

/**
 * Remove Me Controller
 * ------------------------
 * A controller that will dynamically remove
 * the current element from the DOM.
 */
export default class extends Controller {
  remove() {
    this.element.remove();
  }
}
