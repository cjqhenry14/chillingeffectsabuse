import java.io.FileReader;
import java.io.BufferedReader;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.MongoClient;

public class readJson
{
  public static void main(String[] args)
  {
    DB db;
    try {
      MongoClient client = new MongoClient("127.0.0.1", 27017);
      db = client.getDB( "test" );
      DBCollection coll;

      boolean collectionExists = db.collectionExists("chilling");
      if (collectionExists == false) {
        db.createCollection("chilling", null);
      }
      coll = db.getCollection("chilling");
      BufferedReader br = new BufferedReader(new FileReader(args[0]));
      String line;
      
      System.out.println(args[0]);
      while ((line = br.readLine()) != null) {
        //System.out.println(line);
        BasicDBObject doc = (BasicDBObject)com.mongodb.util.JSON.parse(line);
        //System.out.println(doc.toString());
       
        coll.insert(doc);
      }
      br.close();
    } catch (Exception e) {
      System.out.println("exception detected.");
      System.out.println(e.toString());
    }
  }
}
