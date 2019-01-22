db.createUser(
    {
        user: "aquascopeuser",
        pwd: "faea8436",
        roles:[
            {
                role: "readWrite",
                db:   "aquascopedb"
            }
        ]
    }
);
