package furhatos.app.dietcoach

import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder

class dialog {
    companion object {
        /**
         * Sends a response to the dialog manager client so that it can update its internal state
         */
        fun sendResponse(response: String) : String {
            val formattedResponse = response.replace(" ", "%20")
            val url = URL("http://localhost:5000/response" + "?response=" + "\"" + formattedResponse + "\"")
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
                    val output = jsonObject.getString("outputs")

                    return output
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
        fun getStatement(): JSONObject {
            val url = URL("http://localhost:5000/statement")
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

                    return jsonObject
                }
            } catch (e: Exception) {
                System.out.println(e)
                System.err.println("Warning! Could not get results from the dialogue manager! Is the server running?")
                val obj = JSONObject()
                obj.put("outputs", "I'm sorry. I just experienced an error. Could you repeat that?")
                obj.put("gesture", "None")
                obj.put("gestureTiming", false)
                return obj
            }
        }
    }
}