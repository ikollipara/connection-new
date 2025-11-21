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
import ComboBoxController from "./controllers/combobox_controller";
import EditorController from "./controllers/editor_controller";
import QuillController from "./controllers/quill_controller";
import SubmitFormController from "./controllers/submit_form_controller";
import DialogController from "./controllers/dialog_controller";
import FrameReloadController from "./controllers/frame_reload_controller";
import PostDisplayController from "./controllers/post_display_controller";

window.Turbo = Turbo;

Turbo.start();

window.Stimulus = Application.start();

Stimulus.register("combo-box", ComboBoxController);
Stimulus.register("editor", EditorController);
Stimulus.register("quill", QuillController);
Stimulus.register("submit-form", SubmitFormController);
Stimulus.register("dialog", DialogController);
Stimulus.register("frame-reload", FrameReloadController);
Stimulus.register("post-display", PostDisplayController);
