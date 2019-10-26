#[derive(Queryable)]
pub struct Task {
    pub id: uuid::Uuid,
    pub title: String,
    pub parents: Vec<String>,
    pub children: Vec<String>,
    pub tags: Vec<String>,
    pub priority: i32,
    pub entry_date: std::time::SystemTime,
    pub due_date: Option<std::time::SystemTime>,
    pub done_date: Option<std::time::SystemTime>,
    pub modified_date: std::time::SystemTime,
    pub times: Vec<String>,
}

#[derive(Queryable)]
pub struct User {
    pub id: uuid::Uuid,
    pub email: String,
}
