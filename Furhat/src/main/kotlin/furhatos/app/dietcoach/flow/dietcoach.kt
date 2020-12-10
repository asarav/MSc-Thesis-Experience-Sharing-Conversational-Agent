package furhatos.app.dietcoach.flow

import furhatos.app.dietcoach.nlu.*
import furhatos.app.dietcoach.order
import furhatos.flow.kotlin.*
import furhatos.nlu.common.*
import furhatos.app.dietcoach.dialog

val Start = state(Interaction) {
    onEntry {
        furhat.ask(dialog.getStatement())
    }

    onResponse {
        // Query done in query state below, with its result saved here since we're doing a call
        System.out.println(dialog.getResponse())
    }
}