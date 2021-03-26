package ca.mcgill.sis.dmas.kam1n0.app.clone.adata;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;

public class VulnsList {

	/*
	public HashMap<String, Integer> label = new HashMap<String, Integer>() {
		{put("Blockhash", 0);
		put("ERC20", 0);
		put("GasConsumption", 0);
		put("ImplicitVisibility", 0);
		put("IntegerOverflow", 0);
		put("IntegerUnderflow", 0);
		put("Reentrancy", 0);
		put("TimeDependency", 0);
		}
	};
	public HashMap<String, String> name = new HashMap<String, String>() {
		{put("Blockhash", "Blockhash");
		put("ERC20", "ERC-20 Transfer");
		put("GasConsumption", "Gas Consumption");
		put("ImplicitVisibility", "Implicit Visibility");
		put("IntegerOverflow", "Overflow");
		put("IntegerUnderflow", "Underflow");
		put("Reentrancy", "Reentrancy");
		put("TimeDependency", "Time Dependency");
		}
	};

	public VulnsList() {

	}
	*/

	@JsonIgnore
	public Map<String, Integer> vulnsList = new HashMap<>();

	@JsonAnyGetter
	public Map<String, Integer> getVulns() {
		return this.vulnsList;
	}

	@JsonAnySetter
	public void setVulns(String name, Integer isVulns) {
		this.vulnsList.put(name,  isVulns);
	}

	public List<String> getLabelNames() {
		List<String> keyList = new ArrayList<>();
		for(String key : vulnsList.keySet()) {
			keyList.add(key);
		}
		return keyList;
	}

	public Integer getLabel(String key) {
		return vulnsList.get(key);
	}

	public ArrayList<String> getVulnsName() {
		ArrayList<String> vulnsName = new ArrayList<>();
		for(String name : vulnsList.keySet()) {
			if(vulnsList.get(name) == 1) {
				vulnsName.add(name);
			}
		}
		return vulnsName;
	}


}
