namespace BD_1
{
    partial class User
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.table1 = new System.Windows.Forms.DataGridView();
            this.added = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.date = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.result = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.button1 = new System.Windows.Forms.Button();
            this.refresh = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.table1)).BeginInit();
            this.SuspendLayout();
            // 
            // table1
            // 
            this.table1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.table1.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.added,
            this.date,
            this.result});
            this.table1.Location = new System.Drawing.Point(12, 12);
            this.table1.Name = "table1";
            this.table1.ReadOnly = true;
            this.table1.RowHeadersWidth = 35;
            this.table1.Size = new System.Drawing.Size(679, 189);
            this.table1.TabIndex = 0;
            // 
            // added
            // 
            this.added.HeaderText = "Dodano przez";
            this.added.Name = "added";
            this.added.ReadOnly = true;
            // 
            // date
            // 
            this.date.HeaderText = "Data Badania";
            this.date.Name = "date";
            this.date.ReadOnly = true;
            // 
            // result
            // 
            this.result.HeaderText = "Wyniki";
            this.result.Name = "result";
            this.result.ReadOnly = true;
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(713, 12);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(75, 23);
            this.button1.TabIndex = 1;
            this.button1.Text = "Logout";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // refresh
            // 
            this.refresh.Location = new System.Drawing.Point(713, 41);
            this.refresh.Name = "refresh";
            this.refresh.Size = new System.Drawing.Size(75, 23);
            this.refresh.TabIndex = 2;
            this.refresh.Text = "Refresh";
            this.refresh.UseVisualStyleBackColor = true;
            this.refresh.Click += new System.EventHandler(this.refresh_Click);
            // 
            // User
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.refresh);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.table1);
            this.Name = "User";
            this.Text = "Medic App";
            this.Load += new System.EventHandler(this.User_Load);
            ((System.ComponentModel.ISupportInitialize)(this.table1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.DataGridView table1;
        private System.Windows.Forms.DataGridViewTextBoxColumn added;
        private System.Windows.Forms.DataGridViewTextBoxColumn date;
        private System.Windows.Forms.DataGridViewTextBoxColumn result;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button refresh;
    }
}