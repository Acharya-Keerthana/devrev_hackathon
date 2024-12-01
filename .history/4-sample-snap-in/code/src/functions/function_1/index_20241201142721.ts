/*
 * Copyright (c) 2023 DevRev, Inc. All rights reserved.
 */

import { client } from "@devrev/typescript-sdk";

async function handleEvent(
  event: any,
) {
  const devrevPAT = event.context.secrets.service_account_token;
  const API_BASE = event.execution_metadata.devrev_endpoint;
  const devrevSDK = client.setup({
    endpoint: API_BASE,
    token: devrevPAT,
  })
  const workCreated = event.payload.work_created.work;
  const messageInput = event.input_data.global_values.input_field_1;
  let bodyComment = `The work is created with ID: ${workCreated.display_id}\n
  from the owner: ${workCreated.owned_by?.[0]?.full_name}\n
  with title: ${workCreated.title}\n
  having priority: ${workCreated.priority}\n
  and problem description: ${workCreated.body}`;
  const extraComment = event.input_data.global_values.input_field_2;
  const extraNames = event.input_data.global_values.input_field_array;
  if (extraComment) {
    for (let name of extraNames) {
      bodyComment = bodyComment ;
    }
  }
  const body = {
    object: workCreated.id,
    type: 'timeline_comment',
    body:  bodyComment,
  }
  const response = await devrevSDK.timelineEntriesCreate(body as any);
  return response;

}

export const run = async (events: any[]) => {
  console.info('events', JSON.stringify(events), '\n\n\n');
  for (let event of events) {
    const resp = await handleEvent(event);
    console.log(JSON.stringify(resp.data));
  }
};

export default run;