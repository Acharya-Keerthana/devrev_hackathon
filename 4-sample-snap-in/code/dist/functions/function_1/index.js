"use strict";
/*
 * Copyright (c) 2023 DevRev, Inc. All rights reserved.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.run = void 0;
const typescript_sdk_1 = require("@devrev/typescript-sdk");
function handleEvent(event) {
    var _a, _b;
    return __awaiter(this, void 0, void 0, function* () {
        const devrevPAT = event.context.secrets.service_account_token;
        const API_BASE = event.execution_metadata.devrev_endpoint;
        const devrevSDK = typescript_sdk_1.client.setup({
            endpoint: API_BASE,
            token: devrevPAT,
        });
        const workCreated = event.payload.work_created.work;
        const messageInput = event.input_data.global_values.input_field_1;
        let bodyComment = `The work is created with ID: ${workCreated.display_id}\n
  from the owner: ${(_b = (_a = workCreated.owned_by) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.full_name}\n
  with title: ${workCreated.title}\n
  having priority: ${workCreated.priority}\n
  and problem description: ${workCreated.body}`;
        const extraComment = event.input_data.global_values.input_field_2;
        const extraNames = event.input_data.global_values.input_field_array;
        if (extraComment) {
            for (let name of extraNames) {
                bodyComment = bodyComment;
            }
        }
        const body = {
            object: workCreated.id,
            type: 'timeline_comment',
            body: bodyComment,
        };
        const response = yield devrevSDK.timelineEntriesCreate(body);
        return response;
    });
}
const run = (events) => __awaiter(void 0, void 0, void 0, function* () {
    console.info('events', JSON.stringify(events), '\n\n\n');
    for (let event of events) {
        const resp = yield handleEvent(event);
        console.log(JSON.stringify(resp.data));
    }
});
exports.run = run;
exports.default = exports.run;
