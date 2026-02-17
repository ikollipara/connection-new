/**
 * Project:     conneCTION
 * Name:        static/src/controllers/submit_form_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-19
 * Description: submit a form based on a chosen event.
 */

import { Controller } from "@hotwired/stimulus";

/**
 * Submit Form Controller
 * -------------------------
 * A controller to dynamically submit a form using the HTML5 Form API.
 */
export default class extends Controller {
  submit() {
    this.element.requestSubmit();
  }
}
