/**
 * Project:     conneCTION
 * Name:        static/src/controllers/post_display_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-21
 * Description: Display a post as clean HTML
 */

import { Controller } from "@hotwired/stimulus";
import edjsHTML from "editorjs-html";

export default class extends Controller {
  static values = { data: String };

  initialize() {
    this.parser = edjsHTML();
  }

  connect() {
    const data = JSON.parse(document.getElementById(this.dataValue).textContent);
    this.element.innerHTML = this.parser.parse(data);
  }
}
