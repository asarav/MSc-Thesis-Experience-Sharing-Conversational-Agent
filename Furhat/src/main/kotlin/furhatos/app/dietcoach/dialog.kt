package furhatos.app.dietcoach

import org.json.JSONArray
import org.json.JSONObject
import java.lang.Exception
import java.net.HttpURLConnection
import java.net.URL

class dialog {
    companion object {
        /**
         * Returns the next statement outputted by the robot
         */
        private fun getResponse(): String {
            val url = URL("http://localhost:5000/")
            try {
                with(url.openConnection() as HttpURLConnection) {
                    requestMethod = "GET"  // optional default is GET

                    var jsonStr = ""
                    inputStream.bufferedReader().use {
                        it.lines().forEach { line ->
                            jsonStr += line
                        }
                    }

                    val jsonObject = JSONObject(jsonStr)
                    val outputs = ""
                    for (output in jsonObject.getJSONArray("reply")) {
                        val outputValuesList = output as JSONArray
                    }

                    return ""
                }
            } catch (e: Exception) {
                System.err.println("Warning! Could not get results from the dialogue manager! Is the server running?")
                return ""
            }
        }

        /**
         * Returns the next statement outputted by the client
         */
        fun getStatement(): String {
            return ""
        }
    }
}