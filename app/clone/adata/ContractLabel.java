package ca.mcgill.sis.dmas.kam1n0.app.clone.adata;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

public class ContractLabel {
	@JsonIgnore
	public Map<String, FunctionLabel> cntLabel = new HashMap<>();

	@JsonProperty
	public VulnsList source;

	@JsonAnyGetter
	public Map<String, FunctionLabel> getVulns() {
		return this.cntLabel;
	}

	@JsonAnySetter
	public void setVulns(String cntName, FunctionLabel func) {
		this.cntLabel.put(cntName,  func);
	}

	public List<String> getCntNames() {
		List<String> keyList = new ArrayList<>();
		for(String key : cntLabel.keySet()) {
			keyList.add(key);
		}
		return keyList;
	}
	public FunctionLabel getContract(String key) {
		return cntLabel.get(key);
	}

}
