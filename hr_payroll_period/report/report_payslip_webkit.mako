<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for o in objects :
        <center><h2><u>${("Pay Slip")}</u></h2></center>
        %if o.credit_note!=False:
            <center><h2>${("Credit")}</h2></center>
            <center><h2>${("Note")}</h2></center>
        %endif
        <!-- <center>(${o.name or '' | entity})</center> -->
        <table class="basic_table" width="100%" align="center">
            <tr>
                <td width="10%">
                    <b>${_("Period")} </b>
                </td>
                <td width="30%">
                    ${o.payperiod_id.date_start or ''|entity} to ${o.payperiod_id.date_end or ''|entity}
                </td>
                <td width="20%">
                    <b>${_("Reference")} </b>
                </td>
                <td width="30%">
                    ${o.payperiod_id.name or ''|entity} 
                </td>
            </tr>
            <tr>
                <td width="10%">
                    <b>${_("Name")} </b>
                </td>
                <td width="30%">
                    ${o.employee_id.name or '' |entity}
                </td>
                <td width="20">
                    <b>${_("Identification No")} </b>
                </td>
                <td width="30%">
                    ${o.employee_id.identification_id or ''|entity}
                </td>   
            </tr>
            <tr>
                <td width="10%">
                    <b>${_("Designation")} </b>
                </td>
                <td width="30%">
                    ${o.employee_id.job_id.name or ''|entity}
                </td>
                 <td width="20%">
                    <b>${_("Admission Date")} </b>
                </td>
                <td width="30%">
                    ${o.contract_id.date_start or '' |entity}
                </td>
            </tr>  
            <tr>
                <td width="10%">
                    <b>${_("Wage")} </b>
                </td>
                <td width="30%">
                    ${o.contract_id.wage or ''|entity}
                </td>
            </tr>          
        </table>
        <br/><br/>
        <table class="list_table"  width="100%">
            <thead>
                <tr>
                    <th style="text-align:left;">${_("Code")}</th>
                    <th style="text-align:left;">${_("Name")}</th>
                    <th style="text-align:right;">${_("Allocation")}</th>
                    <th style="text-align:right;" >${_("Deduction")}</th>
                </tr>
            </thead>
            %for line in (get_payslip_lines(o.line_ids)):
                <tbody>
                    <tr>
                        <td style="text-align:left;" width="10%">
                            ${line.code or ''|entity}
                        </td>
                        <td style="text-align:left;" width="50%">
                            ${line.name or '' |entity} 
                        </td>
                        <td>
                            %if line.total >= 0:
                                ${formatLang(line.total, currency_obj = o.company_id and o.company_id.currency_id) or 0.0 |entity}
                            %endif
                        </td>
                        <td style="text-align:right;">
                            %if not (line.total >= 0):
                                ${formatLang(line.total, currency_obj = o.company_id and o.company_id.currency_id) or 0.0 |entity}
                            %endif
                        </td>
                    </tr>
                </tbody>                
            %endfor
                <tr>
                    <td style="border-top:1px solid black;"></td>
                    <td style="border-top:1px solid black;"></td>
                    <td style="border-top:1px solid black;">${formatLang(get_allocation_total(o.line_ids))}</td>
                    <td style="border-top:1px solid black;">${formatLang(get_deduction_total(o.line_ids))}</td>
                </tr>
                <tr>
                    <td style="border:0px;" colspan="2"></td>
                    <td style="text-align:left;border:0px;"><b>${_("Total to pay")}</b></td>
                    <td style="text-align:left;border:0px;"><b>${formatLang(get_total_net(o.line_ids))}</b></td>
                </tr>
                
        </table>
        <br/>
        <br/>
        <table width="100%">
            <tr>
                <td width="15%"></td>
                <td width="10%">${_("Signature: ")}</td>
                <td width="20%" style="border-bottom: 1px solid black;"></td>
                <td width="45%"></td>
            </tr>
            <tr>
                <td colspan="4"></td>
            </tr>
            <tr>
                <td width="15%"></td>
                <td width="10%">${_("Ident. Nro: ")}</td>
                <td width="20%" style="border-bottom: 1px solid black;"></td>
                <td width="45%"></td>
            </tr>
        </table>
        <br />
        <!-- <p style="page-break-after:always"></p> -->
    %endfor 
</body>
</html>