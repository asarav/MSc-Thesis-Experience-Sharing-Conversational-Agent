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
        val output : String = dialog.sendResponse(it.text)
        System.out.println(output)

        if (output.equals("End",true)) {
            goto(End)
        } else if(output.equals("Statement", true)) {
            goto(Statement)
        }
        else {
            goto(Second)
        }
    }
}

val Second : State = state(Interaction) {
    onEntry {
        furhat.ask(dialog.getStatement())
    }

    onResponse {
        val output : String = dialog.sendResponse(it.text)
        System.out.println(output)

        if (output.equals("End",true)) {
            goto(End)
        } else if(output.equals("Statement", true)) {
            goto(Statement)
        }
        else {
            goto(Start)
        }
    }
}

val End : State = state(Interaction) {
    onEntry {
        furhat.say(dialog.getStatement())
    }
}

val Statement : State = state(Interaction) {
    onEntry {
        furhat.say(dialog.getStatement())
        delay(500)
        val output : String = dialog.sendResponse("NoResponse")
        if (output.equals("End",true)) {
            goto(End)
        } else if(output.equals("Statement", true)) {
            goto(Statement2)
        }
        else {
            goto(Start)
        }
    }
}

val Statement2 : State = state(Interaction) {
    onEntry {
        furhat.say(dialog.getStatement())
        delay(500)
        val output : String = dialog.sendResponse("No Response")
        if (output.equals("End",true)) {
            goto(End)
        } else if(output.equals("Statement", true)) {
            goto(Statement)
        }
        else {
            goto(Start)
        }
    }
}