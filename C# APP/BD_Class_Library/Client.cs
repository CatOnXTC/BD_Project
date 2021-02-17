using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Text.Json;
using System.Text.Json.Serialization;
using Newtonsoft.Json;
using System.Text.RegularExpressions;
using System.Security.Cryptography;

namespace BD_Class_Library
{
    public class Client
    {
       public string endpoint { get; set; }
       public httpVerbs httpMethod { get; set; }
       public Client() {
            endpoint = string.Empty;
            httpMethod = httpVerbs.GET;
        }
        public enum httpVerbs
        {
            GET,
            POST
        }

        public string Login(string login, string passwd)
        {
            string api_Request = "";
            if (Regex.IsMatch(login, @"^[a-zA-Z0-9]+$"))
            {
                // Logowanie użytkownika po peselu
                if (Regex.IsMatch(login, @"^[0-9]+$"))  
                {
                    if(login.Length!=11)
                    {
                        return "Invalid Login or Password";
                    }
                    api_Request = "http://127.0.0.1:5000/api/users?pesel="+login;
                }
                else // Logowanie administratora po loginie
                {
                    api_Request = "http://127.0.0.1:5000/api/employees?username=" + login;
                }

            }
            else
            {
                return "Invalid Login or Password";
            }
            string hash = "";
            string[] received = makeRequest(api_Request,1);
            if(received.Length!=0 && received!=null && received[0] != null && received[1] != null)
            {
                //TU HASZOWAĆ
                
                using (SHA256 sha256Hash = SHA256.Create())
                {
                    hash = GetHash(sha256Hash, passwd);

                    Console.WriteLine("Verifying the hash...");

                    if (VerifyHash(sha256Hash, passwd, hash))
                    {
                        Console.WriteLine("The hashes are the same.");
                        Console.WriteLine(hash);
                    }
                    else
                    {
                        Console.WriteLine("The hashes are not same.");
                    }
                }
                if (received[0].Equals(login) && received[1].Equals(hash))
                {
                    return "Logged In";
                }
                else
                {
                    return "Invalid Login or Password";
                }
            }
            else
            {
                return "Invalid Login or Password";
            }
          

               
        }
        public string[] GetData(string login, string passwd)
        {
            string api_Request = "";
            if (Regex.IsMatch(login, @"^[a-zA-Z0-9]+$"))
            {
                // Logowanie użytkownika po peselu
                if (Regex.IsMatch(login, @"^[0-9]+$"))
                {
                    if (login.Length == 11)
                    {
                        api_Request = "http://127.0.0.1:5000/api/results?pesel=" + login;
                    }
                    
                }
                else // Logowanie administratora po loginie
                {
                    api_Request = "http://127.0.0.1:5000/api/results?username=" + login;
                }

            }
            string[] received = new string[10];
            received = makeRequest(api_Request,2);
            Console.WriteLine(received);
            //TEST
            return received;


        }
        protected string[] makeRequest(string message, int type)
        {
            string msgResponse = string.Empty;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(message);

            request.Method = httpMethod.ToString();

            try {
                using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                {
                    //GDY RESPONSE NIE JEST 200 OK
                    if (response.StatusCode != HttpStatusCode.OK)
                    {
                        //TODO
                        throw new Exception("Error code: " + response.StatusCode);

                    }
                    using (Stream responseStream = response.GetResponseStream())
                    {
                        if (responseStream != null)
                        {
                            using (StreamReader reader = new StreamReader(responseStream))
                            {
                                String[] resp = new String[100];
                                String jsonResponse = "";
                                int jump = 0;
                                while (jsonResponse != null)
                                {
                                    if(!jsonResponse.Contains("result_file"))
                                    {
                                        jsonResponse = Regex.Replace(jsonResponse, @"[^0-9a-zA-Z_-]+", "");
                                    }
                                   
                                    
                                    if (type == 1)
                                    {

                                        if (jsonResponse.Contains("username"))
                                        {
                                            jsonResponse = jsonResponse.Replace("username", "");
                                            resp[0] = jsonResponse;
                                            break;
                                        }
                                        if (jsonResponse.Contains("pesel"))
                                        {
                                            jsonResponse = jsonResponse.Replace("pesel", "");
                                            resp[0] = jsonResponse;
                                            break;
                                        }
                                        if (jsonResponse.Contains("password"))
                                        {
                                            jsonResponse = jsonResponse.Replace("password", "");
                                            resp[1] = jsonResponse;
                                        }
                                        jsonResponse = reader.ReadLine();
                                    }
                                    else if (type == 2)
                                    {

                                        if (jsonResponse.Contains("pesel"))
                                        {
                                            jsonResponse = jsonResponse.Replace("pesel", "");
                                            resp[0 + jump] = jsonResponse;

                                        }
                                        if (jsonResponse.Contains("result_date"))
                                        {
                                            jsonResponse = jsonResponse.Replace("result_date", "");   
                                            String[] r = jsonResponse.Split('T');
                                            resp[1 + jump] = r[0];
                                        }
                                        if (jsonResponse.Contains("result_file"))
                                        {
                                            jsonResponse = Regex.Replace(jsonResponse, @"[^0-9a-zA-Z\+\\\/\=]+", "");
                                            jsonResponse = jsonResponse.Replace("resultfile", "");
                                            resp[2 + jump] = jsonResponse;
                                        }
                                        if (jsonResponse.Contains("username"))
                                        {
                                            jsonResponse = jsonResponse.Replace("username", "");
                                            resp[3 + jump] = jsonResponse;
                                            jump = jump + 4;

                                        }
                                        jsonResponse = reader.ReadLine();

                                    }

                                }
                                
                                return resp;

                            }
                        }
                        else
                        {
                            return new string[0];
                        }

                    }
                }



            }
                catch(System.Net.WebException)
                {
                    String[] resp = new String[2];
                    resp[0] = "Invalid credentials";
                    resp[1] = "Error";
                    return resp;
                }

        }
        #region Hash
        private static string GetHash(HashAlgorithm hashAlgorithm, string input)
        {

            // Convert the input string to a byte array and compute the hash.
            byte[] data = hashAlgorithm.ComputeHash(Encoding.UTF8.GetBytes(input));

            // Create a new Stringbuilder to collect the bytes
            // and create a string.
            var sBuilder = new StringBuilder();

            // Loop through each byte of the hashed data
            // and format each one as a hexadecimal string.
            for (int i = 0; i < data.Length; i++)
            {
                sBuilder.Append(data[i].ToString("x2"));
            }

            // Return the hexadecimal string.
            return sBuilder.ToString();
        }

        // Verify a hash against a string.
        private static bool VerifyHash(HashAlgorithm hashAlgorithm, string input, string hash)
        {
            // Hash the input.
            var hashOfInput = GetHash(hashAlgorithm, input);

            // Create a StringComparer an compare the hashes.
            StringComparer comparer = StringComparer.OrdinalIgnoreCase;

            return comparer.Compare(hashOfInput, hash) == 0;
        }
        #endregion 
    }
}
