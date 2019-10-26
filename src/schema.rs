table! {
    open (id) {
        id -> Uuid,
        title -> Text,
        parents -> Array<Uuid>,
        children -> Array<Uuid>,
        tags -> Array<Text>,
        priority -> Int2,
        entry_date -> Timestamp,
        due_date -> Nullable<Timestamp>,
        done_date -> Nullable<Timestamp>,
        modified_date -> Timestamp,
        times -> Array<Varchar>,
    }
}

table! {
    users (id) {
        id -> Uuid,
        email -> Varchar,
    }
}

allow_tables_to_appear_in_same_query!(
    open,
    users,
);
