using Application.Data.DataTransfer;
using Application.Data.DataTransfer.RecordType;
using Application.Data.Repositories;
using Contracts;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ModelAPI.Controllers
{
    [ApiController]
    public class RecordTypeController : ControllerBase
    {
        private readonly IRecordTypeRepository _modelTypeRepository;

        public RecordTypeController(IRecordTypeRepository modelTypeRepository)
        {
            _modelTypeRepository = modelTypeRepository;
        }

        [HttpGet(ApiRoutes.RecordType.GetAll)]
        [Produces("application/json")]
        [ProducesResponseType(typeof(EnumerableEnevelope<RecordTypeGetAll>), StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll ()
        {
            var modelTypes = await _modelTypeRepository.GetAllAsync();
            return Ok(modelTypes);
        }
    }
}
