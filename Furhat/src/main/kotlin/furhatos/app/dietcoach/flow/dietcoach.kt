package furhatos.app.dietcoach.flow

import furhatos.app.dietcoach.nlu.*
import furhatos.app.dietcoach.order
import furhatos.flow.kotlin.*
import furhatos.nlu.common.*
import furhatos.app.dietcoach.dialog

val Start : State = state(Interaction) {
    onEntry {
        furhat.ask(dialog.getStatement())
    }

    onResponse {
        // Query done in query state below, with its result saved here since we're doing a call
        val output : String = dialog.sendResponse(it.text)
        System.out.println(output)
        if (output.equals("End",true)) {
            goto(End)
        } else {
            goto(Second)
        }
    }
}

val Second : State = state(Interaction) {
    onEntry {
        furhat.ask(dialog.getStatement())
    }

    onResponse {
        // Query done in query state below, with its result saved here since we're doing a call
        val output : String = dialog.sendResponse(it.text)
        System.out.println(output)
        if (output.equals("End",true)) {
            goto(End)
        } else {
            goto(Start)
        }
    }
}

val End : State = state(Interaction) {
    onEntry {
        furhat.say(dialog.getStatement())
    }
}