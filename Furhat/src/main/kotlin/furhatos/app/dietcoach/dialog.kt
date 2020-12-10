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
        fun getResponse(): String {
            val url = URL("http://localhost:5000/response")
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
                    System.out.println(jsonObject)
                    val outputs = ""
                    print(jsonObject.getString("outputs"))

                    return "Response"
                }
            } catch (e: Exception) {
                System.out.println(e)
                System.err.println("Warning! Could not get results from the dialogue manager! Is the server running?")
                return "INVALID"
            }
        }

        /**
         * Returns the next statement outputted by the client
         */
        fun getStatement(): String {
            val url = URL("http://localhost:5000/response")
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
                    System.out.println(jsonObject)
                    val outputs = ""
                    print(jsonObject.getString("outputs"))

                    return "Response"
                }
            } catch (e: Exception) {
                System.out.println(e)
                System.err.println("Warning! Could not get results from the dialogue manager! Is the server running?")
                return "INVALID"
            }
        }
    }
}