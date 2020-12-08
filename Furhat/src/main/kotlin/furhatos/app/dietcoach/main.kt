package furhatos.app.dietcoach

import furhatos.app.dietcoach.flow.Idle
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class DietCoachSkill : Skill() {
    override fun start() {
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
