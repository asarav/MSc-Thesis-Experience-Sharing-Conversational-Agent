package furhatos.app.dietcoach.flow

import furhatos.app.dietcoach.nlu.*
import furhatos.app.dietcoach.order
import furhatos.flow.kotlin.*
import furhatos.nlu.common.*
import furhatos.app.dietcoach.dialog
import furhatos.autobehavior.userSpeechStartGesture
import furhatos.gestures.Gesture
import furhatos.gestures.Gestures

val Start : State = state(Interaction) {
    onEntry {
        furhat.userSpeechStartGesture = listOf(Gestures.Thoughtful,Gestures.Smile,Gestures.BrowRaise,Gestures.Thoughtful,Gestures.Smile,Gestures.BrowRaise,Gestures.GazeAway,Gestures.Nod)
        val statementObject = dialog.getStatement()
        val statmentOutput = statementObject.getString("outputs")
        val gesture = statementObject.getString("gesture")
        val gestureTiming = statementObject.getBoolean("gestureTiming")
        if (gesture.equals("None", false) && !gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
        furhat.ask(statmentOutput)
        if (gesture.equals("None", false) && gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
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
        val statementObject = dialog.getStatement()
        val statmentOutput = statementObject.getString("outputs")
        val gesture = statementObject.getString("gesture")
        val gestureTiming = statementObject.getBoolean("gestureTiming")
        if (gesture.equals("None", false) && !gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
        furhat.ask(statmentOutput)
        if (gesture.equals("None", false) && gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
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
        val statementObject = dialog.getStatement()
        val statmentOutput = statementObject.getString("outputs")
        val gesture = statementObject.getString("gesture")
        val gestureTiming = statementObject.getBoolean("gestureTiming")
        if (gesture.equals("None", false) && !gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
        furhat.say(statmentOutput)
        if (gesture.equals("None", false) && gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
    }
}

val Statement : State = state(Interaction) {
    onEntry {
        val statementObject = dialog.getStatement()
        val statmentOutput = statementObject.getString("outputs")
        val gesture = statementObject.getString("gesture")
        val gestureTiming = statementObject.getBoolean("gestureTiming")
        if (gesture.equals("None", false) && !gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
        furhat.say(statmentOutput)
        if (gesture.equals("None", false) && gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }

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
        val statementObject = dialog.getStatement()
        val statmentOutput = statementObject.getString("outputs")
        val gesture = statementObject.getString("gesture")
        val gestureTiming = statementObject.getBoolean("gestureTiming")
        if (gesture.equals("None", false) && !gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }
        furhat.say(statmentOutput)
        if (gesture.equals("None", false) && gestureTiming) {
            val gest = handleGesture(gesture)
            furhat.gesture(gest)
        }

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

fun handleGesture(gest: String) : Gesture {
    when (gest) {
        "BigSmile" -> return Gestures.BigSmile
        "Blink" -> return Gestures.Blink
        "Nod" -> return Gestures.Nod
        "BrowFrown" -> return Gestures.BrowFrown
        "BrowRaise" -> return Gestures.BrowRaise
        "CloseEyes" -> return Gestures.CloseEyes
        "ExpressAnger" -> return Gestures.ExpressAnger
        "ExpressDisgust" -> return Gestures.ExpressDisgust
        "ExpressFear" -> return Gestures.ExpressFear
        "ExpressSad" -> return Gestures.ExpressSad
        "GazeAway" -> return Gestures.GazeAway
        "Oh" -> return Gestures.Oh
        "OpenEyes" -> return Gestures.OpenEyes
        "Roll" -> return Gestures.Roll
        "Shake" -> return Gestures.Shake
        "Smile" -> return Gestures.Smile
        "Surprise" -> return Gestures.Surprise
        "Thoughtful" -> return Gestures.Thoughtful
        "Wink" -> return Gestures.Wink
        else -> { // Note the block
            return Gestures.BrowRaise
        }
    }
}