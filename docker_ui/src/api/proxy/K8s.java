package api.proxy;

import java.io.IOException;
import java.text.SimpleDateFormat;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.methods.GetMethod;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Servlet implementation class K8s
 */

public class K8s extends HttpServlet {
	private static final long serialVersionUID = 1L;
    /**
     * @see HttpServlet#HttpServlet()
     */
    public K8s() {
        super();

    }
    
    
    @Override
    public void init(ServletConfig config) throws ServletException {
    	super.init(config);
    	
    	 System.out.println(config.getInitParameter("host"));
    	 Util.server = config.getInitParameter("host")   ;
//       init the get info thread. 
         System.err.println(" STARTING THE GET INFO THREAD .");
    	 Util.getinfo(); 
    }
     
    
	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		 
		String uri  = request.getRequestURI() ;
		String context  = request.getContextPath();
		
		request.getParameter("app");
		
		if(uri.indexOf("K8s") > 0){
			String[] apps  = uri.split("K8s") ;
			String r =null ; 
			if(apps.length > 1 ){
				r =  Util.getAppInfo(apps[1].trim());
			}else{
				r = Util.getAppInfo("namespace-app-name") ;
			}
			if(r != null ){
			response.getWriter().append(r);
			}else{
				try {
					Thread.currentThread().sleep(2000);
					r = Util.getAppInfo("namespace-app-name") ;
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				if(r != null)
				response.getWriter().append(r);
			}
		}else{
			response.setContentType("text/html; charset=UTF-8");
			response.sendRedirect(context +"/K8s");
		}
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
