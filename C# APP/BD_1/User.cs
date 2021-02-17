using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BD_1
{
    //Sprawdzić czy przy null jest zapisz
    public partial class User : Form
    {
        string login, password;
        String[] blobs = new String[100];
        BD_Class_Library.Client client = new BD_Class_Library.Client();

        public User(string log, string pass)
        {
            this.password = pass;
            this.login = log;
            InitializeComponent();
            loadData();
        }
        public User()
        {
            InitializeComponent();
        }

        private void User_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            Application.Restart();
        }

        private void refresh_Click(object sender, EventArgs e)
        {
            table1.Rows.Clear();
            loadData();
        }

        private void table1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            int row = table1.CurrentRow.Index;
            string date = table1.Rows[row].Cells[1].Value.ToString();
            try
            {
                //62051504872___2021-02-17T17_50_31
                byte[] newBytes = Convert.FromBase64String(blobs[row]);
                var folderBrowserDialog1 = new FolderBrowserDialog();
               
                DialogResult result1 = folderBrowserDialog1.ShowDialog();
                if (result1 == DialogResult.OK)
                {
                    string folderName = folderBrowserDialog1.SelectedPath;
                    string filename = folderName +"\\"+ login +"___"+date+".pdf";
                   // string filename2 = folderName+"\\badaniebyte.pdf"; 
                    File.WriteAllBytes(filename, newBytes);
                }
            }
            catch(System.FormatException a)
            {
                Console.WriteLine("Błędny format pliku");
            }
        }

        private string[] loadData()
        {

            string[] response = client.GetData(login, password);
            int i = 1;
            int j = 0;
            blobs = new String[100];
            while (response[i]!=null)
            {
                table1.Rows.Add(); 
                table1.Rows[j].Cells[1].Value = response[i];
                i++;
                if(i%4==0)
                {
                    i++;
                }
                if (response[i] == "null")
                {
                    table1.Rows[j].Cells[2].Value = "Nie umieszczono";
                }
                else
                {
                    table1.Rows[j].Cells[2].Value = "Umieszczono";
                    blobs[j] = response[i];
                }
           
                i++;
                if (i % 4 == 0)
                {
                    i++;
                }
                table1.Rows[j].Cells[0].Value = response[i];
                i++;
                if (i % 4 == 0)
                {
                    i++;
                }
                j++;
            }
  
            return response;
        }
        
    }
}
/*
 private void login_Click(object sender, EventArgs e)
        {
            if(!this.loginBox.Text.Equals("") && !this.passBox.Text.Equals(""))
            {
                this.resp.Text = client.Login(this.loginBox.Text, this.passBox.Text);
                if( this.resp.Text== "Logged In")
                {
                    User user = new User(this.loginBox.Text, this.passBox.Text);
                    this.Hide();
                    user.Show();

                }
            }
            else
            {
                this.resp.Text = "Invalid Credentials";
            }
            
        }
*/