using System;
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
    public partial class User : Form
    {
        string login, password;

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

        private string[] loadData()
        {

            string[] response = client.GetData(login, password);
            table1.Rows.Add();
            table1.Rows[0].Cells[0].Value = response[3];
            table1.Rows[0].Cells[1].Value = response[1];
            if(response[2]=="null")
            {
               table1.Rows[0].Cells[2].Value = "Nie umieszczono";
            }
            else { table1.Rows[0].Cells[1].Value = response[2]; }

            

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