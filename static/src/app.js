/**
 * Project:     conneCTION
 * Name:        static/src/app.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-12
 * Description: Main Frontend Entrypoint
 */

import "./scss/app.scss";
import * as Turbo from "@hotwired/turbo";
import { Application } from "@hotwired/stimulus";

window.Turbo = Turbo;

Turbo.start();

window.Stimulus = Application.start();
